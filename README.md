Drop the package_manager folder inside launcher/game, then add the following to `front_page.rpy`:


```
textbutton _("Install Package") action Jump("package_installer")
```

This adds an interface for installing python packages directly into a renpy project.
