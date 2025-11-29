import "../style/greeting.css"
import {forwardRef, useImperativeHandle, useState} from "react";

export interface GreetingHandle {
  getUsername: () => string
}
const Greeting = forwardRef<GreetingHandle, object>( ({}, ref) => {
  const [selectedUser, setSelectedUser] = useState("charlie")

  const handles = () => {
    return {
      getUsername: () => selectedUser
    }
  }

  useImperativeHandle(ref, handles);

  return (
    <div id="greeting-container">
      <h1>Hi, </h1>
      <select
        value={selectedUser}
        onChange={e => setSelectedUser(e.target.value)}
      >
        <option value="charlie">Charlie</option>
        <option value="james">James</option>
      </select>
    </div>
  )
})

export default Greeting
