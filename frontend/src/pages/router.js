import { createBrowserRouter } from "react-router-dom";
import { GeneralLayout } from "../components/GeneralLayout";
import { ErrorPage } from "./ErrorPage";
import { HomePage } from "./HomePage";
import { S3TreePage } from "./S3TreePage";
import { getBucketsList } from "../services/infoService.ts";

const pages = [
  {
    path: "/",
    element: <GeneralLayout />,
    loader: async () => {
      const data = await getBucketsList();
      return data;
    },
    children: [
      {
        path: "/",
        element: <HomePage />,
      },
      {
        path: "/error",
        element: <ErrorPage />,
      },
      {
        path: "/:bucket_name",
        element: <S3TreePage />,
        loader: async ({ params }) => {
          return params.bucket_name;
        },
      },
    ],
  },
];

const Router = createBrowserRouter(pages);

export default Router;
