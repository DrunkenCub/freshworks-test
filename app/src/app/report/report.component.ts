import { Component, OnInit, ViewChild } from '@angular/core';
import { DataService } from '../data.service';
import { MatTableDataSource } from '@angular/material/table';
import { MatPaginator } from '@angular/material/paginator';

@Component({
  selector: 'app-report',
  templateUrl: './report.component.html',
  styleUrls: ['./report.component.css']
})
export class ReportComponent implements OnInit {

  constructor(private dataService: DataService) { }

  dataSource: any = [];
  displayedColumns = ['user_id', 'location', 'food', 'fed_date', 'total_ducks', 'total_amount']

  @ViewChild(MatPaginator) paginator: MatPaginator | undefined;

  ngOnInit(): void {
    this.dataService.getFeedingData(null).subscribe((data: any) => {
      this.dataSource = new MatTableDataSource(data);
      this.dataSource.paginator = this.paginator;
    })
  }
 
  // applyFilter(event: Event) {
  //   this.dataSource.filterPredicate = (data: any, filter: string) => {
  //     return data.location == filter;
  //   };

  //   const filterValue = (event.target as HTMLInputElement).value;
  //   this.dataSource.filter = filterValue.trim().toLowerCase();
  // }

}
