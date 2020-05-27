INCLUDE(FindPkgConfig)
PKG_CHECK_MODULES(PC_AD2 ad2)

FIND_PATH(
    AD2_INCLUDE_DIRS
    NAMES ad2/api.h
    HINTS $ENV{AD2_DIR}/include
        ${PC_AD2_INCLUDEDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/include
          /usr/local/include
          /usr/include
)

FIND_LIBRARY(
    AD2_LIBRARIES
    NAMES gnuradio-ad2
    HINTS $ENV{AD2_DIR}/lib
        ${PC_AD2_LIBDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/lib
          ${CMAKE_INSTALL_PREFIX}/lib64
          /usr/local/lib
          /usr/local/lib64
          /usr/lib
          /usr/lib64
          )

include("${CMAKE_CURRENT_LIST_DIR}/ad2Target.cmake")

INCLUDE(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(AD2 DEFAULT_MSG AD2_LIBRARIES AD2_INCLUDE_DIRS)
MARK_AS_ADVANCED(AD2_LIBRARIES AD2_INCLUDE_DIRS)
