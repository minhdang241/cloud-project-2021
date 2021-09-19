import { useState } from "react";

interface Props {
  headers: string[];
  sort: Sort;
  setSort: React.Dispatch<React.SetStateAction<Sort>>;
}
export interface Sort {
  by: string;
  order: string;
}
export default function SortHeader({ headers, sort, setSort }: Props) {
  const sortIcon = (head: string) => {
    if (head !== sort.by) {
      return <i className="fas fa-sort ml-2"></i>;
    } else
      return sort.order == "asc" ? <i className="fas fa-sort-up ml-2"></i> : <i className="fas fa-sort-down ml-2"></i>;
  };

  const configSort = (head: string) => {
    let order = "asc";
    let by = head;
    if (sort.by === head) {
      order = sort.order === "asc" ? "desc" : "";
      by = sort.order === "asc" ? by : "";
    }
    setSort({ by, order });
  };

  return (
    <tr>
      {headers.slice(0, 3).map((head, i) => (
        <th role="button" key={i} onClick={() => configSort(head)}>
          {head}
          {sortIcon(head)}
        </th>
      ))}
      <th>{headers[3]}</th>
    </tr>
  );
}
