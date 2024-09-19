import React, { useState, useEffect } from "react";
import { useLoaderData, useNavigate } from "react-router-dom";
import { TfiWrite } from "react-icons/tfi";
import "font-awesome/css/font-awesome.min.css";
import PropagateLoader from "react-spinners/PropagateLoader";
import "./s3tree.scss";
import { formatBytes } from "../../utils/formatBytes.ts";
import { getBucketInfo } from "../../services/infoService.ts";
import { S3Tree } from "./Tree";

export const S3TreePage = () => {
  const bucket_name = useLoaderData();
  const [loading, setLoading] = useState(false);

  const [bucketData, setBucketData] = useState();

  const navigate = useNavigate();

  const retrieveS3Data = async (bucket_name) => {
    setLoading(true);
    const { data, error, message } = await getBucketInfo(bucket_name);
    setLoading(false);
    if (error) {
      console.error(message);
      setBucketData(null);
      navigate("/error");
    } else {
      setBucketData({
        size: formatBytes(data.size),
        datetime: data.datetime,
        isManual: data.manual,
        tree: data.folders.sort((a, b) => b.size - a.size),
      });
    }
  };

  useEffect(() => {
    if (bucket_name) retrieveS3Data(bucket_name);
  }, [bucket_name]);

  return (
    <div className="s3TreePage">
      {!loading && (
        <>
          <h1 className="title">
            {bucket_name}
            {bucketData?.size && (
              <span className="right">{bucketData.size}</span>
            )}
          </h1>
          {bucketData?.isManual && (
            <div data-tooltip="Datos generados manualmente">
              <TfiWrite />
            </div>
          )}
          {bucketData?.datetime && <div>{bucketData.datetime}</div>}
        </>
      )}

      {loading && (
        <div className="loader">
          <PropagateLoader />
        </div>
      )}
      {!loading && bucketData && (
        <div className="tree">
          <S3Tree tree={bucketData.tree ?? []}></S3Tree>
        </div>
      )}
    </div>
  );
};
