import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { DataService } from '../data.service';

@Component({
  selector: 'app-feed',
  templateUrl: './feed.component.html',
  styleUrls: ['./feed.component.css']
})
export class FeedComponent implements OnInit {

  constructor(private router: Router, private dataService: DataService) { }

  date!: string;
  total_amount!: number;
  total_ducks!: number;
  food_id!: number;
  _food_type_id!: number;
  location_id!: number;

  foods!: any;
  foodtypes!: any;
  locations!: any;

  showSpinner: boolean = false;
  is_schedule: boolean = false;

  ngOnInit(): void {
    this.getFoodTypes();
    this.getLocations();
  }

  set food_type_id(value: number) {
    if (value !== this.food_type_id) {
      this._food_type_id = value;
      this.getFoods(value);
    }
  }

  getFoodTypes(): void {
    this.showSpinner = true;
    this.dataService.getFoodTypeData().subscribe((data: any) => {
      this.foodtypes = data;
      this.showSpinner = false;
    })
  }

  getFoods(food_type_id: number): void {
    this.showSpinner = true;
    this.dataService.getFoodData(food_type_id).subscribe((data: any) => {
      this.foods = data;
      this.showSpinner = false;
    })
  }

  getLocations(): void {
    this.showSpinner = true;
    this.dataService.getLocationData().subscribe((data: any) => {
      this.locations = data;
      this.showSpinner = false;
    })
  }

  feed(): void {
    console.log(this.date);
    if (this.is_schedule == true) {
      this.dataService.schedule(this.date, this.location_id, this.food_id, this.total_amount, this.total_ducks).subscribe((data: any) => {
        alert("successfully fed the ducks and schedule added");
      })
    } else {
      this.dataService.feed(this.date, this.location_id, this.food_id, this.total_amount, this.total_ducks).subscribe((data: any) => {
        alert("successfully fed the ducks");
      })
    }
  }

}
