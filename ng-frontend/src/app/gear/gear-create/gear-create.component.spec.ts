import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { GearCreateComponent } from './gear-create.component';

describe('GearCreateComponent', () => {
  let component: GearCreateComponent;
  let fixture: ComponentFixture<GearCreateComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ GearCreateComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(GearCreateComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
