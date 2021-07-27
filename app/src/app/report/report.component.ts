import { Component, OnInit } from '@angular/core';
import { DataService } from '../data.service';
import {MatTableDataSource} from '@angular/material/table';

@Component({
  selector: 'app-report',
  templateUrl: './report.component.html',
  styleUrls: ['./report.component.css']
})
export class ReportComponent implements OnInit {

  constructor(private dataService: DataService) { }

  dataSource: any = [];
  displayedColumns = ['user_id', 'location', 'food', 'fed_date', 'total_ducks', 'total_amount']

  ngOnInit(): void {
    this.dataService.getFeedingData(null).subscribe((data: any) => {
      this.dataSource = new MatTableDataSource(data);
    })
  }

  applyFilter(event: Event) {
    const filterValue = (event.target as HTMLInputElement).value;
    this.dataSource.filter = filterValue.trim().toLowerCase();
  }

}
