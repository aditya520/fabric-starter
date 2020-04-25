# import sys

# def checkPrereqs():
    
#     BLACKLISTED_VERSIONS="^1\."
    
#     # Note, we check configtxlator externally because it does not require a config file, and peer in the
#     # docker image because of FAB-8551 that makes configtxlator return 'development version' in docker
#     LOCAL_VERSION="$(configtxlator version | sed -ne 's/ Version: //p')"
#     DOCKER_IMAGE_VERSION="$(docker run --rm hyperledger/fabric-tools:$IMAGETAG peer version | sed -ne 's/ Version: //p' | head -1)"

#     print("LOCAL_VERSION=" + LOCAL_VERSION)
#     print ("DOCKER_IMAGE_VERSION=" + DOCKER_IMAGE_VERSION)
#     sys.stdout.flush()
    

#     if LOCAL_VERSION != DOCKER_IMAGE_VERSION:
#         print( "=================== WARNING ===================")
#         print( "  Local fabric binaries and docker images are  ")
#         print( "  out of  sync. This may cause problems.       ")
#         print( "===============================================")
        

#         for UNSUPPORTED_VERSION in BLACKLISTED_VERSIONS:
#             print( "LOCAL_VERSION" | grep -q UNSUPPORTED_VERSION
#             if [ $? -eq 0 ]; then
#             print( "ERROR! Local Fabric binary version of $LOCAL_VERSION does not match this newer version of BYFN and is unsupported. Either move to a later version of Fabric or checkout an earlier version of fabric-samples."
#             exit 1
#             fi

#             print( "$DOCKER_IMAGE_VERSION" | grep -q UNSUPPORTED_VERSION
#             if [ $? -eq 0 ]; then
#             print( "ERROR! Fabric Docker image version of $DOCKER_IMAGE_VERSION does not match this newer version of BYFN and is unsupported. Either move to a later version of Fabric or checkout an earlier version of fabric-samples."
#             exit 1
#             fi
#     done
