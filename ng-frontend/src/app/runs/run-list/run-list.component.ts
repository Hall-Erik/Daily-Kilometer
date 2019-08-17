import { Component, OnInit } from '@angular/core';

import { RunService } from '../../services/run.service';
import { Run } from '../../models/run';

@Component({
  selector: 'app-run-list',
  templateUrl: './run-list.component.html',
  styleUrls: ['./run-list.component.css']
})
export class RunListComponent implements OnInit {
  runs: Run[];

  constructor(private runService: RunService) { }

  ngOnInit() {
    this.runService.get_runs().subscribe((runs) => {
      this.runs = runs;
    });
  }

}
