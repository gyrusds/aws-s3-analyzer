import { memo, useState } from "react";
import { formatBytes } from "../../utils/formatBytes.ts";
import { S3Tree } from "./Tree";

export const S3TreeNode = memo(
  ({ folder }) => {
    const [isExpanded, setIsExpanded] = useState(false);

    const handleToggle = (e) => {
      e.preventDefault();
      e.stopPropagation();
      setIsExpanded((expanded) => !expanded);
    };

    return (
      <details
        key={folder.id}
        disabled={folder?.children?.length === 0}
        onToggle={handleToggle}
      >
        <summary>
          <i
            className={`fa ${isExpanded ? "fa-folder-open" : "fa-folder"}`}
          ></i>
          <div className="selector"></div>
          {folder.name}
          <span className="right">({formatBytes(folder.size)})</span>
        </summary>
        {isExpanded && folder.children && (
          <S3Tree tree={folder.children.sort((a, b) => b.size - a.size)} />
        )}
      </details>
    );
  },
  (prevProps, nextProps) => {
    return prevProps.folder.id === nextProps.folder.id;
  }
);
