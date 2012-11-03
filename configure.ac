AC_INIT([gnome-getting-started-docs], [3.6.2],
        [http://bugzilla.gnome.org/enter_bug.cgi?product=gnome-getting-started-docs])
AM_INIT_AUTOMAKE([1.11 tar-ustar dist-xz no-dist-gzip])
AM_SILENT_RULES([yes])
AC_PROG_CC

YELP_HELP_INIT

AM_MAINTAINER_MODE([enable])

PKG_CHECK_MODULES(PLAYER, [clutter-gst-1.0 clutter-x11-1.0])

if test "$GCC" = "yes"; then
        CFLAGS="\
        -Wall \
        -Wchar-subscripts -Wmissing-declarations -Wmissing-prototypes \
        -Wnested-externs -Wpointer-arith \
        -Wcast-align -Wsign-compare \
        -Werror $CFLAGS"
fi

AC_SUBST(CFLAGS)

AM_CONFIG_HEADER(config.h)
AC_CONFIG_FILES([
Makefile
getting-started/Makefile
player/Makefile
])
AC_OUTPUT
