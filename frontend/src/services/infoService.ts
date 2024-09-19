import axios from "axios";

const api_url = "http://0.0.0.0:8000";

/**
 * Retrieves the list of buckets from the server.
 * @returns A promise that resolves with the bucket list data.
 */
export const getBucketsList = async () => {
  return new Promise((resolve, reject) => {
    axios
      .get(`${api_url}`)
      .then((response) => {
        return response.data;
      })
      .then((data) => resolve(data))
      .catch((error) => {
        console.error("Error fetching summary:", error);
        reject(error);
      });
  });
};

/**
 * Retrieves information about a specific bucket.
 * @param bucket_name - The name of the bucket to retrieve information for.
 * @returns A promise that resolves to the bucket information.
 */
export const getBucketInfo = async (bucket_name: string) => {
  return new Promise((resolve, reject) => {
    axios
      .get(`${api_url}/${bucket_name}`)
      .then((response) => {
        return {
          data: response.data,
          error: false,
        };
      })
      .then((data) => resolve(data))
      .catch((error) => {
        console.error(`Error fetching ${bucket_name}:`, error);
        return {
          data: [],
          error: true,
          message: error,
        };
      });
  });
};
