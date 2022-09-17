import { IdrissCrypto } from "idriss-crypto/lib/browser";

export default async function isTwitterResolved(address) {
  const obj = new IdrissCrypto();
  const reverse = await obj.reverseResolve(
    "0x4a3755eb99ae8b22aafb8f16f0c51cf68eb60b85"
  );
  return reverse;
}
