# Copyright 2011,2012,2016 Free Software Foundation, Inc.
#
# This file is part of GNU Radio
#
# GNU Radio is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
#
# GNU Radio is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with GNU Radio; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.

########################################################################
# Setup library
########################################################################
include(GrPlatform) #define LIB_SUFFIX

include_directories(${Boost_INCLUDE_DIR})
link_directories(${Boost_LIBRARY_DIRS})

list(APPEND AD2_AnalogOut_Play_sources
)

set(AD2_AnalogOut_Play_sources "${AD2_AnalogOut_Play_sources}" PARENT_SCOPE)
if(NOT AD2_AnalogOut_Play_sources)
	MESSAGE(STATUS "No C++ sources... skipping lib/")
	return()
endif(NOT AD2_AnalogOut_Play_sources)

add_library(gnuradio-AD2_AnalogOut_Play SHARED ${AD2_AnalogOut_Play_sources})
target_link_libraries(gnuradio-AD2_AnalogOut_Play ${Boost_LIBRARIES} ${GNURADIO_ALL_LIBRARIES})
set_target_properties(gnuradio-AD2_AnalogOut_Play PROPERTIES DEFINE_SYMBOL "gnuradio_AD2_AnalogOut_Play_EXPORTS")

if(APPLE)
    set_target_properties(gnuradio-AD2_AnalogOut_Play PROPERTIES
        INSTALL_NAME_DIR "${CMAKE_INSTALL_PREFIX}/lib"
    )
endif(APPLE)

########################################################################
# Install built library files
########################################################################
include(GrMiscUtils)
GR_LIBRARY_FOO(gnuradio-AD2_AnalogOut_Play RUNTIME_COMPONENT "AD2_AnalogOut_Play_runtime" DEVEL_COMPONENT "AD2_AnalogOut_Play_devel")

########################################################################
# Build and register unit test
########################################################################
include(GrTest)

include_directories(${CPPUNIT_INCLUDE_DIRS})

list(APPEND test_AD2_AnalogOut_Play_sources
    ${CMAKE_CURRENT_SOURCE_DIR}/test_AD2_AnalogOut_Play.cc
    ${CMAKE_CURRENT_SOURCE_DIR}/qa_AD2_AnalogOut_Play.cc
)

add_executable(test-AD2_AnalogOut_Play ${test_AD2_AnalogOut_Play_sources})

target_link_libraries(
  test-AD2_AnalogOut_Play
  ${GNURADIO_RUNTIME_LIBRARIES}
  ${Boost_LIBRARIES}
  ${CPPUNIT_LIBRARIES}
  gnuradio-AD2_AnalogOut_Play
)

GR_ADD_TEST(test_AD2_AnalogOut_Play test-AD2_AnalogOut_Play)

########################################################################
# Print summary
########################################################################
message(STATUS "Using install prefix: ${CMAKE_INSTALL_PREFIX}")
message(STATUS "Building for version: ${VERSION} / ${LIBVER}")

