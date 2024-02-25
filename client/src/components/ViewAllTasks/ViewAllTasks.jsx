import axios from "axios";
import React, { useState, useEffect } from "react";

import { baseUrl } from "../../utils/config";

const ViewAllTasks = () => {
  const [ViewAllTasks, setViewAllTasks] = useState([]);

  //   useEffect(() => {
  //     const fetchAllTasks = async () => {
  //       const { data } = await axios.get(`${baseUrl}/get_tasks`);
  //       console.log(data.message);
  //     };

  //     fetchAllTasks();
  //   }, [ViewAllTasks]);

  return (
    <section>
      <h1>View your tasks for today</h1>
    </section>
  );
};

export default ViewAllTasks;
