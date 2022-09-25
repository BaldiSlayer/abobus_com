function push() {
    console.log(5555555);

    fetch('/sms', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: {'n': 'b', 'sd': 'sadasda'}
    });
}