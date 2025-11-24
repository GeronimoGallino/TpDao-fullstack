import { ComponentFixture, TestBed } from '@angular/core/testing';

import { RepAlqPer } from './rep-alq-per';

describe('RepAlqPer', () => {
  let component: RepAlqPer;
  let fixture: ComponentFixture<RepAlqPer>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [RepAlqPer]
    })
    .compileComponents();

    fixture = TestBed.createComponent(RepAlqPer);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
