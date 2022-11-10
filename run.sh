#!/bin/bash

if [ $1 = "-help" ]
then
printf "\n\t-mesh: Only converts .geo file to .msh and adjusts the boundaries \n\t -all: Runs meshing and application\n"
else

printf "Script executed from: ${PWD}"

helper="/Users/zeemarquez/openfoam/assignment/helpers.py"
casepath="${PWD}"
printf "Case Path: ${casepath}"

application=$(python3 ${helper} application ${casepath})

if [ $application = "error" ] 
then
    echo "ERROR: Make sure the runof.sh file is executed in the correct case folder"
else
    if [ $1 = "meshonly" ] 
    then 
        printf "\n------------- Running Mesh only -------------\n\n"
        gmsh mesh.geo -format msh2 -3 -o mesh.msh
        openfoam -c "gmshToFoam mesh.msh"
        python3 ${helper} boundary ${casepath}
        openfoam -c checkMesh
    elif [ $1 = "all" ]
    then
        printf "\n------------- Running Meshing + Application -------------\n\n"
        gmsh mesh.geo -format msh2 -3 -o mesh.msh
        openfoam -c "gmshToFoam mesh.msh"
        python3 ${helper} boundary ${casepath}
        printf "\nOpenFOAM Application:${application}\n"
        openfoam -c checkMesh
        rm 0/yPlus
        openfoam -c "decomposePar -force"
        openfoam -c "mpirun -oversubscribe -np 4 ${application} -parallel > log"
        openfoam -c reconstructPar
        openfoam -c "${application} -postProcess -latestTime -func yPlus"
    else
        printf "\n------------- Running Application only -------------\n\n"

        printf "\nOpenFOAM Application:${application}\n"
        rm 0/yPlus
        openfoam -c "decomposePar -force"
        openfoam -c "mpirun -oversubscribe -np 4 ${application} -parallel > log"
        openfoam -c reconstructPar
        openfoam -c "${application} -postProcess -latestTime -func yPlus"

    fi
fi
fi