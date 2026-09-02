document.addEventListener('click', function (event) {
    if (window.innerWidth >= 992) {
        return;
    }

    const submenuToggle = event.target.closest('.custom-navbar .dropdown-submenu > .dropdown-item');
    const dropdownToggle = event.target.closest('.custom-navbar .nav-item.dropdown > .nav-link.dropdown-toggle');

    if (!submenuToggle && !dropdownToggle) {
        return;
    }

    event.preventDefault();
    event.stopImmediatePropagation();

    if (submenuToggle) {
        const submenu = submenuToggle.closest('.dropdown-submenu');
        const menu = submenu.querySelector(':scope > .dropdown-menu');
        const isOpen = submenu.classList.contains('show');

        document.querySelectorAll('.custom-navbar .dropdown-submenu').forEach(function (item) {
            item.classList.remove('show');
            const childMenu = item.querySelector(':scope > .dropdown-menu');
            if (childMenu) childMenu.style.display = 'none';
        });

        if (!isOpen) {
            submenu.classList.add('show');
            if (menu) menu.style.display = 'block';
        }
        return;
    }

    const dropdown = dropdownToggle.closest('.nav-item.dropdown');
    const menu = dropdown.querySelector(':scope > .dropdown-menu');
    const isOpen = dropdown.classList.contains('show');

    document.querySelectorAll('.custom-navbar .nav-item.dropdown').forEach(function (item) {
        item.classList.remove('show');
        const itemMenu = item.querySelector(':scope > .dropdown-menu');
        if (itemMenu) itemMenu.style.display = 'none';
    });

    if (!isOpen) {
        dropdown.classList.add('show');
        if (menu) menu.style.display = 'block';
    }
}, true);
