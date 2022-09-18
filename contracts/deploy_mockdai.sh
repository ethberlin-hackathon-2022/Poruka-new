if [ -f .env ]
then
  export $(cat .env | xargs)
else
    echo "No .env file"
    exit 0
fi

forge create --rpc-url $FOUNDRY_ETH_URL --private-key $FOUNDRY_ETH_PRIVATE_KEY src/DaiMock.sol:MockDai
forge inspect ./src/DaiMock.sol:MockDai abi > MockDai_abi.json
