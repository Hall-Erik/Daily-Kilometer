import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';

import { User } from '../../models/user';
import { Run } from 'src/app/models/run';

import { UserService } from '../../services/user.service';
import { RunService } from '../../services/run.service';

@Component({
  selector: 'app-run-edit',
  templateUrl: './run-edit.component.html',
  styleUrls: ['./run-edit.component.css']
})
export class RunEditComponent implements OnInit {
  user: User = this.userService.user.getValue();
  run: Run;

  constructor(private route: ActivatedRoute,
              private router: Router,
              private userService: UserService,
              private runService: RunService) { }

  ngOnInit() {
    this.userService.user.subscribe(user => this.user = user);
    let id = this.route.snapshot.paramMap.get('id');
    this.runService.get_run(+id).subscribe(run => this.run = run);
  }

  update(run: Run) {
    run.pk = this.run.pk;
    this.runService.update_run(run).subscribe(() => {
      this.router.navigate(['index']);
    })
  }
}
