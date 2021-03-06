from optutil import Config
import coreoptions
import os

PRELUDE = """
.. This page has been automatically generated by `_options/generate.py`!

Configuration Options
=====================

This is a (partial!) list of the various configuration options uWSGI supports. See the documentation for each feature for further details.

""".strip()

def render_rst(config):
    output = [PRELUDE]
    write = output.append

    for section in config.sections:
        write("")
        write("%s" % section.name)
        write("-" * len(section.name))
        write("")
        if section.docs:
            write(u".. seealso::")
            write(u"")
            for doc in section.docs:
                write(u"   :doc:`%s`" % doc)
            write("")

        write(".. list-table::")
        write("   :header-rows: 1")
        write("   ")
        write("   * - Option")
        write("     - Argument")
        write("     - Description")
        
        for opt in section.options:
            write("   * - %s" % ", ".join("``%s``" % name for name in opt.names))
            write("     - %s" % opt.get_argument())
            write("     - %s" % opt.get_description())
            if opt.docs:
                write("       See %s for more information." % ", ".join(u":doc:`%s`" % topic for topic in opt.docs))


    return output

def write_output(output):
    target_file = os.path.realpath(os.path.join(os.path.dirname(__file__), "..", "Options.rst"))
    with file(target_file, "wb") as out_file:
        out_file.write("\n".join(output).encode("UTF-8"))

def main():
    print "Reading..."
    config = Config()
    coreoptions.add_core_options(config)
    # XXX: Add other modules?

    print "Rendering..."
    rst_lines = render_rst(config)
    print "Writing..."
    write_output(rst_lines)



if __name__ == '__main__':
    main()