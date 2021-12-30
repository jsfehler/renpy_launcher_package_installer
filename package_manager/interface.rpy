style l_input_frame is l_default:
    background Solid("#070707")
    xminimum 600
    xmaximum 600
    yminimum 36
    ymaximum 36
    xoffset 16

style l_input_text:
    xoffset 8
    yalign 0.5
    size 18
    color INPUT_COLOR

style l_input_button is l_default:
    background Solid("#070707")
    xminimum 600
    xmaximum 600
    yminimum 36
    ymaximum 36

style l_input_settings_label:
    size 16
    xalign 0.0
    color TEXT

style l_input_settings_text:
    size 14
    xalign 0.0
    color TEXT

style l_input_settings_description:
    size 12
    xalign 0.0
    color TEXT


default persistent.python_executable_path = 'C:\Python39\python.exe'
default persistent.python_package_path = 'python_packages'


define package_installer_settings_items = [
    {
        'title': _('Python Executable Path'),
        'description': _('Location of the python executable to use for installing packages.'),
        'value': "python_executable_path",
    },
    {
        'title': _('Target Directory'),
        'description': _("Location, inside the current project's game directory, to install packages."),
        'value': "python_package_path",
    },
]

screen package_installer_settings():
    default input_focus = 0
    
    frame:
        style "l_root"
        
        vbox:
            spacing 16

            text _('Package Installer Settings') style "l_input_settings_label"
        
            vbox:
                spacing 16

                for idx, item in enumerate(package_installer_settings_items):

                    vbox:
                        text item['title'] style "l_input_settings_text"
                        text item['description'] style "l_input_settings_description"

                        frame:
                            style "l_input_frame"
                            if input_focus == idx:
                                input:
                                    style "l_input_text"
                                    value FieldInputValue(persistent, item['value'], returnable=False)
                                    copypaste True
                            else:
                                textbutton getattr(persistent, item['value']):
                                    style "l_input_button"
                                    text_style "l_input_text"
                                    action SetScreenVariable("input_focus", idx)
                

    textbutton _("Return") action Call("package_installer") style "l_left_button"


screen package_installer_input():
    default package_name = ''
    default input_focus = 0

    frame:
        style "l_root"
        
        vbox:
            label _("Install a third party python package")
            text _("By default, packages will be fetched from the Python Package Index.") style "l_text"

        vbox:

            frame:
                style_group "l_info"

                vbox:
                    text _('Package Name')

                    frame:
                        style "l_input_frame"
                        xalign 0.5
                        if input_focus == 1:
                            input:
                                style "l_input_text"
                                value ScreenVariableInputValue("package_name", returnable=True)
                                copypaste True
                        else:
                            textbutton package_name:
                                style "l_input_button"
                                text_style "l_input_text"
                                action SetScreenVariable("input_focus", 1)


    textbutton _("Package Installer Settings"):
        style "l_right_button"
        action Call("package_installer_settings")

    textbutton _("Return") action Jump("front_page") style "l_left_button"


screen package_installer_output(output):
    text _("Output:")
    frame:
        style_group "l_info"
        ymaximum 400

        viewport:
            mousewheel True
            draggable True
            scrollbars "vertical"

            python:
                try:
                    info = str(output)
                    output_display = Text(info, substitute=False)
                
                except Exception as e:
                    output_display = str(info)

            text output_display
    
    textbutton _("Return") action Jump("front_page") style "l_left_button"


label package_installer_settings:
    call screen package_installer_settings
    return


label package_installer:
    call screen package_installer_input

    $ package_name = _return

    python:
        from package_manager.package_manager import install_python_package
        
        package_installer_config = {
            'executable_path': persistent.python_executable_path,
            'package_path': persistent.python_package_path,
        }
        result = install_python_package(package_name, package_installer_config)

    call screen package_installer_output(result)
