import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {
  dataframes: any[] = [];

  constructor(private http: HttpClient) {}

  ngOnInit() {
    this.fetchDataFrames();
  }

  fetchDataFrames() {
    this.http.get('http://localhost:5000/dataframes').subscribe((data: any) => {
      this.dataframes = data;
    });
  }
}
