import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { faEdit, faTrash } from '@fortawesome/free-solid-svg-icons';
import { faPaw, faRoad, faMountain, faStopwatch, faDungeon, faFlagCheckered } from '@fortawesome/free-solid-svg-icons';

import { User } from '../../models/user';
import { Run } from 'src/app/models/run';

import { AlertService } from '../../services/alert.service';
import { UserService } from '../../services/user.service';
import { RunService } from '../../services/run.service';

@Component({
  selector: 'app-run-detail',
  templateUrl: './run-detail.component.html',
  styleUrls: ['./run-detail.component.css']
})
export class RunDetailComponent implements OnInit {
  faTrash = faTrash
  faEdit = faEdit
  faPaw = faPaw;
  faRoad = faRoad;
  faMountain = faMountain;
  faStopwatch = faStopwatch;
  faDungeon = faDungeon;
  faFlagCheckered = faFlagCheckered;
  
  run: Run;
  user: User = this.userService.user.getValue();

  constructor(private route: ActivatedRoute,
              private router: Router,
              private runService: RunService,
              private userService: UserService,
              private alertService: AlertService) { }

  ngOnInit() {
    let run_id = this.route.snapshot.paramMap.get('id');
    this.runService.get_run(+run_id).subscribe((run) => {
      this.run = run;
    });
    this.userService.user.subscribe(user => this.user = user);
    this.userService.get_user().subscribe();
  }

  get run_type() {
    switch (this.run.run_type) {
      case 'Canicross':
        return faPaw;
      case 'Road run':
        return faRoad;
      case 'Long run':
        return faStopwatch;
      case 'Trail run':
        return faMountain;
      case 'Race':
        return faFlagCheckered;
      case 'Treadmill':
        return faDungeon;
    }
    return '';
  }

  delete() {
    if (confirm('Are you sure you want to delete?')) {
      this.runService.delete_run(+this.run.pk).subscribe(() => {
        this.router.navigate(['index']);
        this.alertService.success("Run deleted.");
      });
    }
  }
}
