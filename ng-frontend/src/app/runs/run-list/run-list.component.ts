import { Component, OnInit } from '@angular/core';

import { RunService } from '../../services/run.service';
import { UserService } from '../../services/user.service';
import { Run } from '../../models/run';
import { User } from '../../models/user';

@Component({
  selector: 'app-run-list',
  templateUrl: './run-list.component.html',
  styleUrls: ['./run-list.component.css']
})
export class RunListComponent implements OnInit {
  runs: Run[];
  user: User = this.userService.user.getValue();

  constructor(private runService: RunService,
              private userService: UserService) { }

  ngOnInit() {
    this.runService.get_runs().subscribe(runs => this.runs = runs);
    this.userService.user.subscribe(user => this.user = user);
  }

  submit(run: Run) {
    this.runService.create_run(run).subscribe(() => {
      this.runService.get_runs().subscribe(runs => this.runs = runs);
    });
  }

  delete(run: Run) {
    if (confirm('Are you sure you want to delete?')) {
      this.runService.delete_run(run.pk).subscribe(() => {
        this.runService.get_runs().subscribe(runs => this.runs = runs);
      });
    }
  }
}
