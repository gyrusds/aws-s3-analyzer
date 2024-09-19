import React from "react";
import { useOutletContext } from "react-router-dom";
import "./home.scss";

export const HomePage = () => {
  const items = useOutletContext();
  return (
    <main>
      {items.error ? (
        <div className="error">
          <div>No hay buckets</div>
          <div>
            <img src="pulp-fiction-wtf.gif" alt="No hay buckets" />
          </div>
        </div>
      ) : (
        <div className="home">
          <h3>Selecciona un bucket de la lista para ver su desglose.</h3>
        </div>
      )}
    </main>
  );
};
