import { TestBed } from '@angular/core/testing';

import { RepAlqPer } from './rep-alq-per';

describe('RepAlqPer', () => {
  let service: RepAlqPer;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(RepAlqPer);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
