import "../style/greeting.css"
import {useEffect, useState} from "react";
import {UserDetails, type UserDetailsDTO} from "../interfaces/UserDetails.ts";

export interface GreetingProps {
  callback: (a: string) => void
}
const Greeting = ({callback}: GreetingProps) => {
  const [selectedUser, setSelectedUser] = useState("charlie")
  const [points, setPoints] = useState(0)

  useEffect(() => {
    fetch(`http://localhost:5000/api/get-user-details?username=${selectedUser}`).then(async res => {
      if (res.ok) {
        const json: UserDetailsDTO = await res.json()
        const userDetails = UserDetails.fromJson(json)

        setPoints(userDetails.points)
      }
    })
  }, [selectedUser]);

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
