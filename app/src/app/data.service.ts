import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class DataService {

    // Due to time restrictions I have only used one service class. Ideally for each domain there should be one service

  private REST_API_SERVER = "http://localhost:5000";

  constructor(private httpClient: HttpClient) { }

  public login(email:string, password: string){
    const login = {
      'email': email,
      'password': password
    }
    return this.httpClient.post(this.REST_API_SERVER + "/auth/login", login);
  }
  
  public signup(email:string, password: string, fullname: string, admin: boolean){
    const signup = {
      'email': email,
      'password': password,
      'fullname': fullname,
      'admin': admin
    }
    return this.httpClient.post(this.REST_API_SERVER + "/auth/signup", signup);
  }
}
