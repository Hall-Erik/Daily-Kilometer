import { Component, OnInit, HostListener } from '@angular/core';

import { AlertService } from '../../services/alert.service';
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
  mobile: boolean;
  runs: Run[];
  next: string = '';
  user: User = this.userService.user.getValue();

  constructor(private runService: RunService,
              private userService: UserService,
              private alertService: AlertService) { }

  ngOnInit() {
    this.get_runs();
    this.userService.user.subscribe(user => this.user = user);
    this.mobile = (window.screen.width === 360) ? true : false;
  }

  get_runs(next_page: string = '') {
    this.runService.get_runs((next_page) ? next_page : null)
    .subscribe(runList => {
      if (next_page) {
        Array.prototype.push.apply(this.runs, runList.results);
      } else {
        this.runs = runList.results;
      }
      this.next = runList.next;
    });
    this.userService.get_user().subscribe();
  }

  @HostListener('window:scroll')
  onWindowScroll() {
    let pos = Math.ceil(window.innerHeight + window.scrollY);
    let max = document.documentElement.scrollHeight;
    if (pos >= max && this.next) {
      let next = this.next;
      this.next = '';
      this.get_runs(next);
    }
  }

  @HostListener('window:resize')
  onresize() {
    this.mobile = (window.screen.width === 360) ? true : false;
  }

  submit(run: Run) {
    this.runService.create_run(run).subscribe(() => {
      this.get_runs();
      this.alertService.success("Run created.");
    });
  }

  delete(run: Run) {
    if (confirm('Are you sure you want to delete?')) {
      this.runService.delete_run(run.pk).subscribe(() => {
        this.get_runs();
        this.alertService.success("Run deleted.");
      });
    }
  }
}
