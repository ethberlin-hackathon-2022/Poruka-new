if [ -f .env ]
then
  export $(cat .env | xargs)
else
    echo "No .env file"
    exit 0
fi

#forge create --rpc-url $FOUNDRY_ETH_URL --private-key $FOUNDRY_ETH_PRIVATE_KEY src/Treasury.sol:Treasury --constructor-args $OWNER_TRESUARY_PUBLIC_KEY
forge create --rpc-url $FOUNDRY_ETH_URL --private-key $FOUNDRY_ETH_PRIVATE_KEY src/CreditLine.sol:CreditLine --constructor-args $DAI_ADDRESS $TRESUARY
#forge script script/deploy.sol:DeployScript --rpc-url $FOUNDRY_ETH_URL --broadcast --verify -vvvv

