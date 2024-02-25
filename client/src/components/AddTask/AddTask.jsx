import React, { useEffect, useState } from "react";
import axios from "axios";

import { baseUrl } from "../../utils/config";

const AddTask = () => {
  const currentDate = new Date();
  const dateToday = `${currentDate.getDate()}-${currentDate.getMonth()}-${currentDate.getFullYear()}`;
  const timeNow = `${currentDate.getHours()}:${currentDate.getMinutes()}`;
  const title = "";
  const [taskDetails, setTaskDetails] = useState({
    title: "",
    start_date: "",
    start_time: "",
    end_date: "",
    end_time: "",
    tag: "",
  });

  const dynamicTextDetailsExtraction = (e) => {
    setTaskDetails((prevState) => ({
      ...prevState,
      title: e.target.value,
    }));
    setTimeout(async () => {
      generateTextDetails();
      console.log(taskDetails);
    }, 5000);
  };

  const generateTextDetails = async () => {
    const { data } = await axios.get(`http://localhost:5000/text-ai`, {
      params: { title: taskDetails.title },
    });
    console.log(data);
    setTaskDetails((prevState) => ({
      ...prevState,
      tag: data.tag,
    }));

    data.date &&
      setTaskDetails((prevState) => ({
        ...prevState,
        end_date: data.date,
      }));

    data.time &&
      setTaskDetails((prevState) => ({
        ...prevState,
        end_time: data.time,
      }));
  };

  const handleSubmitData = async () => {
    const submitData = {
      summary: taskDetails.title
        ? taskDetails.title
        : alert("Please enter title!"),
      start:
        taskDetails.start_date && taskDetails.start_time
          ? `${taskDetails.start_date}T${taskDetails.start_time}`
          : alert("Please enter start date and time for your task!"),
      end:
        taskDetails.end_date && taskDetails.end_time
          ? `${taskDetails.end_date}T${taskDetails.end_time}`
          : alert("Please enter end date and time for your task!"),
      tag: taskDetails.tag ? taskDetails.tag : "miscellaneous",
    };
    console.log(submitData);
    const { data } = await axios.post(`${baseUrl}/enter_new_task`, submitData);
    console.log(data);
  };

  return (
    <section className="flex flex-col items-center justify-center mt-5">
      <form className="flex flex-col w-[55%] clear-start bg-white p-5 rounded-lg">
        <div className="flex flex-row items-center bg-white justify-between">
          <input
            type="text"
            placeholder="Add Task"
            value={taskDetails.title}
            onChange={dynamicTextDetailsExtraction}
            on
            className="mb-5 bg-transparent border-2 border-sky-400 rounded-l-md p-2 w-[90%]"
          />
          <input
            type="button"
            value="Create"
            onClick={generateTextDetails}
            className="rounded-r-md bg-sky-400 p-[8px] text-xl w-30 cursor-pointer mb-5 items-center font-semibold text-white"
          />
        </div>

        <div className="bg-white flex flex-row justify-between">
          <input
            type="date"
            min={dateToday}
            max="2030-12-31"
            value={taskDetails.start_date}
            onChange={(e) =>
              setTaskDetails((prevState) => ({
                ...prevState,
                start_date: e.target.value,
              }))
            }
            className="mb-5 bg-transparent border-2 border-sky-400 rounded-md p-2"
          />
          <input
            type="time"
            value={taskDetails.start_time}
            onChange={(e) =>
              setTaskDetails((prevState) => ({
                ...prevState,
                start_time: e.target.value + ":00",
              }))
            }
            className="mb-5 bg-transparent border-2 border-sky-400 rounded-md p-2 w-30"
          />

          <input
            type="date"
            min={dateToday}
            max="2030-12-31"
            value={taskDetails.end_date}
            placeholder="End date"
            onChange={(e) =>
              setTaskDetails((prevState) => ({
                ...prevState,
                end_date: e.target.value,
              }))
            }
            className="mb-5 bg-transparent border-2 border-sky-400 rounded-md p-2"
          />

          <input
            type="time"
            value={taskDetails.end_time}
            onChange={(e) =>
              setTaskDetails((prevState) => ({
                ...prevState,
                end_time: e.target.value + ":00",
              }))
            }
            className="mb-5 bg-transparent border-2 border-sky-400 rounded-md p-2 w-30"
          />
        </div>
        <select
          className="mb-5 bg-transparent border-2 border-sky-400 rounded-md p-2 w-30"
          value={taskDetails.tag}
          onChange={(e) =>
            setTaskDetails((prevState) => ({
              ...prevState,
              tag: e.target.value,
            }))
          }
        >
          <option value="none" className="bg-white">
            Select a tag
          </option>
          <option value="work" className="bg-white">
            work
          </option>
          <option value="personal" className="bg-white">
            personal
          </option>
          <option value="health" className="bg-white">
            health
          </option>
          <option value="shopping" className="bg-white">
            shopping
          </option>
          <option value="study" className="bg-white">
            study
          </option>
          <option value="home" className="bg-white">
            home
          </option>
          <option value="finances" className="bg-white">
            finances
          </option>
          <option value="social" className="bg-white">
            social
          </option>
          <option value="family" className="bg-white">
            family
          </option>
          <option value="career" className="bg-white">
            career
          </option>
          <option value="hobbies" className="bg-white">
            hobbies
          </option>
          <option value="events" className="bg-white">
            events
          </option>
          <option value="appointments" className="bg-white">
            appointments
          </option>
          <option value="miscellaneous" className="bg-white">
            miscellaneous
          </option>
        </select>
        <div className="flex flex-row items-center bg-white justify-center">
          <input
            type="button"
            value="Add Task"
            onClick={handleSubmitData}
            className="rounded-md bg-sky-400 p-1 text-xl w-40 cursor-pointer items-center font-semibold text-white"
          />
        </div>
      </form>
    </section>
  );
};

export default AddTask;
