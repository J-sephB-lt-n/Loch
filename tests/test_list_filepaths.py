from loch.filesystem import filter_filepaths

from pathlib import Path


def test_list_filepaths():
    """
    client/
    ├── .vscode/
    │   └── settings.json
    │
    ├── .config/
    │   └── tailwind.config.js
    │
    ├── public/
    │   ├── favicon.ico
    │   └── index.html
    │
    ├── src/
    │   ├── _shared/
    │   │   ├── constants.js
    │   │   └── types.js
    │   │
    │   ├── _partials/
    │   │   ├── Header.jsx
    │   │   └── Footer.jsx
    │   │
    │   ├── assets/
    │   │   ├── images/
    │   │   │   └── logo.svg
    │   │   └── fonts/
    │   │       └── Roboto.woff2
    │   │
    │   ├── components/
    │   │   ├── Button/
    │   │   │   ├── Button.jsx
    │   │   │   └── Button.module.css
    │   │   └── Modal/
    │   │       ├── Modal.jsx
    │   │       └── Modal.module.css
    │   │
    │   ├── pages/
    │   │   ├── Home/
    │   │   │   └── Home.jsx
    │   │   └── About/
    │   │       └── About.jsx
    │   │
    │   ├── hooks/
    │   │   └── useWindowSize.js
    │   │
    │   ├── styles/
    │   │   ├── _variables.css
    │   │   └── global.css
    │   │
    │   ├── utils/
    │   │   └── formatDate.js
    │   │
    │   ├── App.jsx
    │   ├── main.jsx
    │   └── router.jsx
    │
    ├── .env
    ├── .gitignore
    ├── index.html                 # sometimes duplicated at root for certain build tools
    ├── package.json
    ├── README.md
    ├── vite.config.js
    """
    paths: list[Path] = [
        Path(x)
        for x in (
            "client/.vscode/settings.json",
            "client/.config/tailwind.config.js",
            "client/public/index.html",
            "client/public/favicon.ico",
            "client/src/_shared/constants.js",
            "client/src/_shared/types.js",
            "client/src/_partials/Header.jsx",
            "client/src/_partials/Footer.jsx",
            "client/src/assets/images/logo.svg",
            "client/src/assets/fonts/Roboto.woff2",
            "client/src/components/Button/Button.jsx",
            "client/src/components/Button/Button.module.css",
            "client/src/components/Modal/Modal.jsx",
            "client/src/components/Modal/Modal.module.css",
            "client/src/pages/Home/Home.jsx",
            "client/src/pages/About/About.jsx",
            "client/src/hooks/useWindowSize.js",
            "client/src/styles/_variables.css",
            "client/src/styles/global.css",
            "client/src/utils/formatDate.js",
            "client/src/App.jsx",
            "client/src/main.jsx",
            "client/src/router.jsx",
            "client/.env",
            "client/.gitignore",
            "client/index.html",
            "client/package.json",
            "client/README.md",
            "client/vite.config.js",
        )
    ]
    assert (
        len(
            filter_filepaths(
                paths,
                exclude_dot_folders=False,
                exclude_leading_underscore_folders=False,
            )
        )
        == 29
    )
    assert (
        len(
            filter_filepaths(
                paths,
                # exclude_dot_folders=False,
                exclude_leading_underscore_folders=False,
            )
        )
        == 25
    )
    assert (
        len(
            filter_filepaths(
                paths,
                exclude_dot_folders=False,
                # exclude_leading_underscore_folders=False,
            )
        )
        == 24
    )
    assert filter_filepaths(paths) == filter_filepaths(
        paths, include_folders=[Path("client/")]
    )
    assert filter_filepaths(
        paths,
        include_folders=[
            Path("client/.config"),
            Path("client/src/styles"),
            Path("src/pages"),
        ],
    ) == [Path("client/src/styles/global.css")]
    assert filter_filepaths(paths, include_folders=[Path("client/src")]) + [
        Path("client/index.html"),
        Path("client/package.json"),
        Path("client/README.md"),
        Path("client/vite.config.js"),
    ] == filter_filepaths(paths, exclude_folders=[Path("client/public")])
