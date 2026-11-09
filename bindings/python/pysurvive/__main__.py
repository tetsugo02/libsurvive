import subprocess

import pysurvive
import sys
import os
try:
    from gooey import Gooey, GooeyParser
except ImportError:
    sys.exit("the pysurvive GUI needs gooey: pip install 'pysurvive[gui]'")

@Gooey(tabbed_groups=True,
       image_dir=os.path.dirname(os.path.realpath(__file__)) + "/images",
       use_cmd_args=True,
       program_name="pysurvive",
       richtext_controls=True,
       clear_before_run=True)
def main():
    parser = pysurvive.create_argument_parser(GooeyParser())

    args = parser.parse_args()

    if args.websocketd:
        subprocess.run(["survive-websocketd"] + sys.argv[1:])
        return

    print(" ".join(sys.argv))
    actx = pysurvive.SimpleContext(sys.argv)

    while actx.Running():
        pass


if __name__ == '__main__':
    main()
