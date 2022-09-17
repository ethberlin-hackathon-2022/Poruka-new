import { MagnifyingGlassIcon } from "@heroicons/react/20/solid";
import { ReactComponent as Plus } from "../Images/plus.svg";

export default function Lend() {
  const people = [
    // {
    //   name: "Calvin Hawkins",
    //   email: "calvin.hawkins@example.com",
    //   image:
    //     "https://pbs.twimg.com/profile_images/378800000857919980/lHqPIZza_normal.png",
    // },
    // {
    //   name: "Kristen Ramos",
    //   email: "kristen.ramos@example.com",
    //   image:
    //     "https://images.unsplash.com/photo-1550525811-e5869dd03032?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=2&w=256&h=256&q=80",
    // },
    // {
    //   name: "Ted Fox",
    //   email: "ted.fox@example.com",
    //   image:
    //     "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=2&w=256&h=256&q=80",
    // },
  ];

  return (
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
              {people.map((person) => (
                <li key={person.email} className="flex py-4">
                  <div className="flex w-full justify-between">
                    <div className="flex">
                      <img
                        className="h-10 w-10 rounded-full"
                        src={person.image}
                        alt=""
                      />
                      <div className="ml-3">
                        <p className="text-sm font-medium text-gray-900">
                          {person.name}
                        </p>
                        <p className="text-sm text-gray-500">{person.email}</p>
                      </div>
                    </div>
                    <button
                      type="button"
                      className="inline-flex items-center rounded border border-gray-300 bg-white px-2.5 py-1.5 text-xs font-medium text-gray-700 shadow-sm hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2"
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
            {people.length === 0 ? (
              <>
                <div className="flex items-center justify-center mt-20">
                  <div className="grid place-items-center">
                    <Plus />
                    <p className="mt-5">Add people from the list</p>
                  </div>
                </div>
              </>
            ) : (
              <>Y'a une liste</>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
