if (POLICY CMP0068)
    cmake_policy(SET CMP0068 NEW)
    set(CMAKE_BUILD_WITH_INSTALL_NAME_DIR ON)
endif ()

if(POLICY CMP0075)
    cmake_policy(SET CMP0075 NEW)
endif()

if(POLICY CMP0077)
    cmake_policy(SET CMP0077 NEW)
endif()

if (POLICY CMP0116)
    cmake_policy(SET CMP0116 NEW)
endif ()

set(MLIR_DIR "D://dev//libs//mlir-15//lib//cmake//mlir")

find_package(MLIR REQUIRED CONFIG)
if (MLIR_FOUND)
    message(STATUS "Using MLIRConfig.cmake in: ${MLIR_DIR}")

    list(APPEND CMAKE_MODULE_PATH ${MLIR_CMAKE_DIR})

    include(TableGen)
    include(AddMLIR)

    include_directories(${MLIR_INCLUDE_DIRS})
endif ()