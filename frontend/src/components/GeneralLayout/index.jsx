import { Outlet, useLoaderData } from "react-router-dom";
import SideBar from "../SideBar";
import TopBar from "../TopBar";
import "./generalLayout.scss";

export const GeneralLayout = () => {
  const items = useLoaderData();
  return (
    <>
      <TopBar />
      <div className="page">
        <SideBar />
        <Outlet context={items} />
      </div>
    </>
  );
};
