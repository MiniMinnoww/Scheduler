import "../style/greeting.css"
import {useEffect, useState} from "react";

export interface GreetingProps {
  callback: (a: string) => void
  points: number
}
const Greeting = ({callback, points}: GreetingProps) => {
  const [selectedUser, setSelectedUser] = useState("charlie")


  useEffect(() => {
    console.log(points)
  }, [selectedUser, points]);

  const setUser = (v: string) => {
    setSelectedUser(v)
    callback(v)
  }

  return (
    <>
      <div id="greeting-container">
        <h1>Hi, </h1>
        <select
          value={selectedUser}
          onChange={e => setUser(e.target.value)}
        >
          <option value="alice">Alice</option>
          <option value="bob">Bob</option>
          <option value="charlie">Charlie</option>
          <option value="diana">Diana</option>
          <option value="eve">Eve</option>
          <option value="frank">Frank</option>
        </select>
      </div>
      <h2>You have {points} points!</h2>
    </>
  )
}

export default Greeting
