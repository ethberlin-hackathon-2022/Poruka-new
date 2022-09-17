import { IdrissCrypto } from "idriss-crypto/lib/browser";

export default async function isTwitterResolved(address) {
  const obj = new IdrissCrypto();
  const reverse = await obj.reverseResolve(address);
  return reverse;
}
