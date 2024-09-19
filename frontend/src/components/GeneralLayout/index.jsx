import { Outlet } from "react-router-dom";
import SideBar from "../SideBar";
import TopBar from "../TopBar";
import "./generalLayout.scss";

export const GeneralLayout = () => {
  return (
    <>
      <TopBar />
      <div className="page">
        <SideBar />
        <Outlet />
      </div>
    </>
  );
};
