import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';

import { User } from '../../models/user';
import { Run } from 'src/app/models/run';

import { UserService } from '../../services/user.service';
import { RunService } from '../../services/run.service';

@Component({
  selector: 'app-run-detail',
  templateUrl: './run-detail.component.html',
  styleUrls: ['./run-detail.component.css']
})
export class RunDetailComponent implements OnInit {
  run: Run;
  user: User = this.userService.user.getValue();

  constructor(private route: ActivatedRoute,
              private runService: RunService,
              private userService: UserService) { }

  ngOnInit() {
    let run_id = this.route.snapshot.paramMap.get('id');
    this.runService.get_run(+run_id).subscribe((run) => {
      this.run = run;
    });
    this.userService.user.subscribe(user => this.user = user);
  }

  delete() {
    console.log('Do a delete.');
  }
}
