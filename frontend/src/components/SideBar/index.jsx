import React, { useState, useEffect } from "react";
import { NavLink, useLoaderData, useLocation } from "react-router-dom";
import { IconContext } from "react-icons";
import { TfiWrite } from "react-icons/tfi";

import "./sideBar.scss";
import { formatBytes } from "../../utils/formatBytes.ts";

export default function SideBar() {
  const items = useLoaderData();
  const [sidebar, setSidebar] = useState(false);
  const [pathName, setPathName] = useState("");
  const location = useLocation();
  const showSidebar = () => setSidebar(!sidebar);

  useEffect(() => {
    setPathName(location.pathname.replace("/", ""));
  }, [location.pathname]);

  return (
    <aside>
      <IconContext.Provider value={{ color: "undefined" }}>
        <nav className="nav-menu">
          <ul className="nav-menu-items" onClick={showSidebar}>
            {items.data.map((item, idx) => {
              return (
                <NavLink
                  key={idx}
                  to={`/${item.bucket_name}`}
                  className="nav-link"
                >
                  <li
                    className="nav-item"
                    data-active={pathName === item.bucket_name}
                  >
                    <span className="nav-item__name">{item.bucket_name}</span>
                    {item.status === "manual" && (
                      <span
                        className="nav-item__status"
                        data-tooltip="Datos manuales"
                      >
                        <TfiWrite />
                      </span>
                    )}
                    <span className="nav-item__size">
                      {formatBytes(item.size)}
                    </span>
                  </li>
                </NavLink>
              );
            })}
          </ul>
        </nav>
      </IconContext.Provider>
    </aside>
  );
}
