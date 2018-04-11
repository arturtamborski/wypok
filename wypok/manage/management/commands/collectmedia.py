from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from optparse import make_option
import os
import sys
import glob
import shutil
try:
    set
except NameError:
    from sets import Set as set # Python 2.3 fallback


class Command(BaseCommand):
    media_dirs = ['media']
    ignore_apps = ['django.contrib.admin']
    exclude = ['CVS', '.*', '*~']
    option_list = BaseCommand.option_list + (
        make_option('--media-root', default=settings.MEDIA_ROOT, dest='media_root', metavar='DIR',
            help="Specifies the root directory in which to collect media files."),
        make_option('-n', '--dry-run', action='store_true', dest='dry_run',
            help="Do everything except modify the filesystem."),
        make_option('-d', '--dir', action='append', default=media_dirs, dest='media_dirs', metavar='NAME',
            help="Specifies the name of the media directory to look for in each app."),
        make_option('-e', '--exclude', action='append', default=exclude, dest='exclude', metavar='PATTERNS',
            help="A space-delimited list of glob-style patterns to ignore. Use multiple times to add more."),
        make_option('-l', '--link', action='store_true', dest='link',
            help="Create a symbolic link to each file instead of copying."),
        make_option('-i', '--interactive', action='store_true', dest='interactive',
            help="Ask before modifying files and selecting from multiple sources."
        )
    )
    help = 'Collect media files from installed apps in a single media directory.'
    args = '[appname ...]'
    
    def handle(self, *app_labels, **options):
        if not app_labels:
            app_labels = settings.INSTALLED_APPS
        media_root = options.get('media_root', settings.MEDIA_ROOT)
        interactive = options.get('interactive', False)
        dry_run = options.get('dry_run', False)
        if dry_run:
            print("\n    DRY RUN! NO FILES WILL BE MODIFIED.")
        # This mapping collects files that may be copied.  Keys are what the
        # file's path relative to `media_root` will be when copied.  Values
        # are a list of 2-tuples containing the the name of the app providing
        # the file and the file's absolute path.  The list will have a length
        # greater than 1 if multiple apps provide a media file with the same
        # relative path.
        media_files = {}
        for app in app_labels:
            if app not in self.ignore_apps:
                for rel_path, abs_path in self.handle_app(app, **options):
                    media_files.setdefault(rel_path, []).append((app, abs_path))
        if not media_files:
            print("\nNo media found.")
            return
        
        # Try to copy in some predictable order.
        destinations = list(media_files)
        destinations.sort()
        for destination in destinations:
            sources = media_files[destination]
            first_source, other_sources = sources[0], sources[1:]
            if interactive and other_sources:
                first_app = first_source[0]
                app_sources = dict(sources)
                print("\nThe file %r is provided by multiple apps:" % destination)
                print("\n".join(["    %s" % app for (app, source) in sources]))
                message = "Enter the app that should provide this file [%s]: " % first_app
                while True:
                    app = raw_input(message)
                    if not app:
                        app, source = first_source
                        break
                    elif app in app_sources:
                        source = app_sources[app]
                        break
                    else:
                        print("The app %r does not provide this file." % app)
            else:
                app, source = first_source
            print("\nSelected %r provided by %r." % (destination, app))
            self.process_file(source, destination, media_root, **options)
    
    def handle_app(self, app, **options):
        if isinstance(app, basestring):
            app = __import__(app, {}, {}, [''])
        media_dirs = options.get('media_dirs')
        exclude = options.get('exclude')
        app_root = os.path.dirname(app.__file__)
        for media_dir in media_dirs:
            app_media = os.path.join(app_root, media_dir)
            if os.path.isdir(app_media):
                prefix_length = len(app_media) + len(os.sep)
                for root, dirs, files in os.walk(app_media):
                    # Filter `dirs` and `files` based on the exclusion pattern.
                    dirs[:] = self.filter_names(dirs, exclude=exclude)
                    files[:] = self.filter_names(files, exclude=exclude)
                    for filename in files:
                        absolute_path = os.path.join(root, filename)
                        relative_path = absolute_path[prefix_length:]
                        yield (relative_path, absolute_path)
    
    def process_file(self, source, destination, root, link=False, **options):
        dry_run = options.get('dry_run', False)
        interactive = options.get('interactive', False)
        destination = os.path.join(root, destination)
        
        if not dry_run:
            # Get permission bits and ownership of `root`.
            try:
                root_stat = os.stat(root)
            except os.error as e:
                mode = 0777 # Default for `os.makedirs` anyway.
                uid = gid = None
            else:
                mode = root_stat.st_mode
                uid, gid = root_stat.st_uid, root_stat.st_gid
            destination_dir = os.path.dirname(destination)
            try:
                # Recursively create all the required directories, attempting
                # to use the same mode as `root`.
                os.makedirs(destination_dir, mode)
            except os.error as e:
                # This probably just means the leaf directory already exists,
                # but if not, we'll find out when copying or linking anyway.
                pass
            else:
                os.lchown(destination_dir, uid, gid)
        if link:
            success = self.link_file(source, destination, interactive, dry_run)
        else:
            success = self.copy_file(source, destination, interactive, dry_run)
        if success and None not in (uid, gid):
            # Try to use the same ownership as `root`.
            os.lchown(destination, uid, gid)
    
    def copy_file(self, source, destination, interactive=False, dry_run=False):
        "Attempt to copy `source` to `destination` and return True if successful."
        if interactive:
            exists = os.path.exists(destination) or os.path.islink(destination)
            if exists:
                print("The file %r already exists." % destination)
                if not self.prompt_overwrite(destination):
                    return False
        print("Copying %r to %r." % (source, destination))
        if not dry_run:
            try:
                os.remove(destination)
            except os.error as e:
                pass
            shutil.copy2(source, destination)
            return True
        return False
    
    def link_file(self, source, destination, interactive=False, dry_run=False):
        "Attempt to link to `source` from `destination` and return True if successful."
        if sys.platform == 'win32':
            message = "Linking is not supported by this platform (%s)."
            raise os.error(message % sys.platform)
        
        if interactive:
            exists = os.path.exists(destination) or os.path.islink(destination)
            if exists:
                print("The file %r already exists." % destination)
                if not self.prompt_overwrite(destination):
                    return False
        if not dry_run:
            try:
                os.remove(destination)
            except os.error as e:
                pass
        print("Linking to %r from %r." % (source, destination))
        if not dry_run:
            os.symlink(source, destination)
            return True
        return False
    
    def prompt_overwrite(self, filename, default=True):
        "Prompt the user to overwrite and return their selection as True or False."
        yes_values = ['Y']
        no_values = ['N']
        if default:
            prompt = "Overwrite? [Y/n]: "
            yes_values.append('')
        else:
            prompt = "Overwrite? [y/N]: "
            no_values.append('')
        while True:
            overwrite = raw_input(prompt).strip().upper()
            if overwrite in yes_values:
                return True
            elif overwrite in no_values:
                return False
            else:
                print("Select 'Y' or 'N'.")
    
    def filter_names(self, names, exclude=None, func=glob.fnmatch.filter):
        if exclude is None:
            exclude = []
        elif isinstance(exclude, basestring):
            exclude = exclude.split()
        else:
            exclude = [pattern for patterns in exclude for pattern in patterns.split()]
        excluded_names = set(
            [name for pattern in exclude for name in func(names, pattern)]
        )
        return set(names) - excluded_names
