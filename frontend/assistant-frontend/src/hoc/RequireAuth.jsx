import React from 'react'
import { Navigate } from 'react-router'
import store from '../store/Store'
const RequireAuth = ({children}) => {
  const auth = store.isAuthenticated
  if (!auth) {
    return <Navigate to='/StartPage' />
  }
  return children
}

export default RequireAuth
