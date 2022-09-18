import { MagnifyingGlassIcon } from "@heroicons/react/20/solid";
import { ReactComponent as Plus } from "../Images/plus.svg";
import { XMarkIcon } from "@heroicons/react/20/solid";
import { useState } from "react";
import fetchFollowers from "../helpers/fetchFollowers";
import { useEffect, useCallback } from "react";
import { BigNumber, ethers } from "ethers";
import abi from '../utils/creditline_abi.json';
import erc20Abi from '../utils/erc20_abi.json';
import { CreditLineContractAddress, StableCoinContractAddress } from '../utils/config';

export default function Lend({ allFollowers, userAddress, setAllFollowers, twitterId, signer, injectedProvider }) {
  const [listPeople, setListPeople] = useState([]);

  useEffect(() => {
    try {
      console.log("twitter id", twitterId);
      if (twitterId) {
        const fetchAll = async () => {
          const result = await fetchFollowers(twitterId);
          setAllFollowers([...result]);
        };
        fetchAll();
      }
    } catch (error) {
      console.log(error);
    }
  }, [twitterId, setAllFollowers]);

  const handleChange = (i, e) => {
    let newElement = [...listPeople];
    newElement[i][e.target.name] = e.target.value;
    setListPeople(newElement);
  };

  let handleAdd = (person) => {
    setListPeople([...listPeople, person]);
  };

  const handleSubmit = useCallback(async (event) => {
    event.preventDefault();
    const inputs = [...listPeople];
    console.log("Owners of the multisig =>", inputs);

    const daiContract = (new ethers.Contract(StableCoinContractAddress, erc20Abi, injectedProvider)).connect(signer);

    if ((await daiContract.allowance(userAddress, CreditLineContractAddress)).eq(0)) {
      await daiContract.approve(CreditLineContractAddress, BigNumber.from(2).pow(255));
    }

    const creditLineContract = (new ethers.Contract(CreditLineContractAddress, abi, injectedProvider)).connect(signer);
    (await creditLineContract.Create([
      [
        [
          // AMOUNT
          1, 
          // INTEREST
          0, 
        ],
        // Borrower
        '0xaBbAb368BC46F24019858df77D3202bf931A12a3'
      ]
    ]));
  }, [signer, listPeople, userAddress, injectedProvider]);

  return (
    <>
      <div className="mx-20 mt-20">
        <div className="w-full text-center">
          <p className="font-bold text-4xl">Who would you like to lend to?</p>
          <p className="text-xl font-light leading-10">
            Select from the list of people you follow on Twitter
          </p>
        </div>
        <div className="flex justify-center mt-5">
          <div className="overflow-hidden rounded-lg bg-white shadow mr-10 w-full">
            <div className="px-5 py-5 sm:p-6">
              <p className="font-normal leading-10 text-3xl">
                People you follow on Twitter
              </p>
              <button
                onClick={(e) => {
                  handleSubmit(e);
                }}
              >
                CHECK
              </button>
              <div className="mt-5">
                <label htmlFor="search" className="sr-only">
                  Search
                </label>
                <div className="relative mt-1 border-gray-300 rounded-md shadow-sm">
                  <div
                    className="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3"
                    aria-hidden="true"
                  >
                    <MagnifyingGlassIcon
                      className="mr-3 h-4 w-4 text-gray-400"
                      aria-hidden="true"
                    />
                  </div>
                  <input
                    type="text"
                    name="search"
                    id="search"
                    className="block w-full h-10 rounded-md border-gray-300 pl-9 focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
                    placeholder="Search for people you follow on Twitter"
                  />
                </div>
              </div>
              <ul role="list" className="divide-y divide-gray-200">
                {allFollowers?.map((person, index) => (
                  <li key={person.id} className="flex py-4">
                    <div className="flex w-full justify-between">
                      <div className="flex">
                        <img
                          className="h-10 w-10 rounded-full"
                          src={
                            person.img ||
                            "https://pbs.twimg.com/profile_images/378800000857919980/lHqPIZza_normal.png"
                          }
                          alt=""
                        />
                        <div className="ml-3">
                          <p className="text-sm font-medium text-gray-900">
                            {person.username || "oo"}
                          </p>
                          <p className="text-sm text-gray-500">
                            {person.id || "ouou"}
                          </p>
                        </div>
                      </div>
                      <button
                        type="button"
                        className="inline-flex items-center rounded border border-gray-300 bg-white px-2.5 py-1.5 text-xs font-medium text-gray-700 shadow-sm hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2"
                        onClick={() => handleAdd(person)}
                      >
                        Add
                      </button>
                    </div>
                  </li>
                ))}
              </ul>
            </div>
          </div>
          <div className="overflow-hidden rounded-lg bg-white shadow w-full">
            <div className="px-4 py-5 sm:p-6">
              <div className="flex justify-between">
                <p className="font-normal leading-10 text-3xl">
                  People selected for lending
                </p>
                {true ? (
                  <button className="inline-flex items-center rounded-md border border-transparent bg-blue-700 px-4 py-2 text-sm font-medium text-white">
                    Review
                  </button>
                ) : (
                  <span className="inline-flex items-center rounded-md border border-transparent bg-gray-200 px-4 py-2 text-sm font-medium text-white">
                    Review
                  </span>
                )}
              </div>
              {listPeople.length === 0 ? (
                <>
                  <div className="flex items-center justify-center mt-20">
                    <div className="grid place-items-center">
                      <Plus />
                      <p className="mt-5">Add people from the list</p>
                    </div>
                  </div>
                </>
              ) : (
                <>
                  <div className="">
                    <div className="mt-8 flex flex-col">
                      <div className="-my-2 -mx-4 overflow-x-auto sm:-mx-6 lg:-mx-8">
                        <div className="inline-block min-w-full py-2 align-middle md:px-6 lg:px-8">
                          <table className="min-w-full divide-y divide-gray-300">
                            <thead>
                              <tr>
                                <th
                                  scope="col"
                                  className="py-3.5 pl-4 pr-3 text-left text-sm font-semibold text-gray-900 sm:pl-6 md:pl-0"
                                >
                                  Name
                                </th>
                                <th
                                  scope="col"
                                  className="py-3.5 px-3 text-left text-sm font-semibold text-gray-900"
                                >
                                  Amount
                                </th>
                                <th
                                  scope="col"
                                  className="py-3.5 px-3 text-left text-sm font-semibold text-gray-900"
                                >
                                  Interest
                                </th>
                              </tr>
                            </thead>
                            <tbody className="divide-y divide-gray-200">
                              {listPeople?.map((person, index) => (
                                <tr key={person.id}>
                                  <li key={person.id} className="flex py-4">
                                    <div className="flex w-full justify-between">
                                      <div className="flex">
                                        <img
                                          className="h-10 w-10 rounded-full"
                                          src={person.img}
                                          alt=""
                                        />
                                        <div className="ml-3">
                                          <p className="text-sm font-medium text-gray-900">
                                            {person.username}
                                          </p>
                                          <p className="text-sm text-gray-500">
                                            {person.id}
                                          </p>
                                        </div>
                                      </div>
                                    </div>
                                  </li>
                                  <td className="whitespace-nowrap py-4 px-3 text-sm text-gray-500">
                                    <div>
                                      <select
                                        id="amount"
                                        name="amount"
                                        className="mt-1 block w-full rounded-md border-gray-300 py-2 pl-3 pr-10 text-base focus:border-indigo-500 focus:outline-none focus:ring-indigo-500 sm:text-sm"
                                        onChange={(e) => {
                                          handleChange(index, e);
                                        }}
                                        value={100}
                                      >
                                        <option>100</option>
                                        <option>200</option>
                                        <option>300</option>
                                      </select>
                                    </div>
                                  </td>
                                  <td className="whitespace-nowrap py-4 px-3 text-sm text-gray-500">
                                    <div>
                                      <select
                                        id="interest"
                                        name="interest"
                                        className="mt-1 block w-full rounded-md border-gray-300 py-2 pl-3 pr-10 text-base focus:border-indigo-500 focus:outline-none focus:ring-indigo-500 sm:text-sm"
                                        onChange={(e) => {
                                          handleChange(index, e);
                                        }}
                                        value={0}
                                      >
                                        <option>0</option>
                                        <option>0.5</option>
                                        <option>1</option>
                                      </select>
                                    </div>
                                  </td>
                                  <td className="whitespace-nowrap py-4 px-3 text-gray-500">
                                    <button
                                      type="button"
                                      className="rounded-md py-2 px-6 font-medium text-gray-800"
                                    >
                                      <XMarkIcon className="h-5 w-5" />
                                    </button>
                                  </td>
                                </tr>
                              ))}
                            </tbody>
                          </table>
                        </div>
                      </div>
                    </div>
                  </div>
                </>
              )}
            </div>
          </div>
        </div>
      </div>
    </>
  );
}
