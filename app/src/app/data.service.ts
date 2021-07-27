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

  public getFeedingData(filtering: any){
    return this.httpClient.get(this.REST_API_SERVER + "/feed/feed");
  }

  public getLocationData(){
    return this.httpClient.get(this.REST_API_SERVER + "/location/");
  }

  public getFoodTypeData(){
    return this.httpClient.get(this.REST_API_SERVER + "/food/foodtypes");
  }

  public getFoodData(food_type_id: number){
    return this.httpClient.get(this.REST_API_SERVER + "/food/foods?food_type_id=" + food_type_id);
  }

  public feed(fed_date: string, location_id: number, food_id: number, total_amount:number, total_ducks:number){
    const feed = {
      "fed_date": fed_date,
      "location_id": location_id,
      "food_id": food_id,
      "total_amount": total_amount,
      "total_ducks": total_ducks
    }
    return this.httpClient.post(this.REST_API_SERVER + "/feed/feed", feed);
  }
}
