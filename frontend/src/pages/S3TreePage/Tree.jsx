import { memo } from "react";
import { S3TreeNode } from "./TreeNode";

export const S3Tree = memo(
  ({ tree }) => {
    return tree.map((folder) => <S3TreeNode key={folder.id} folder={folder} />);
  },
  (prevProps, nextProps) => {
    return prevProps.tree === nextProps.tree;
  }
);
