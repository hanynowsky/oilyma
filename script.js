
		<script>
			$(document).ready(function() {
				$( "#auto" ).change( function() {
					var auto_val = this.value;
					if (auto_val == 1) {
						$("#approval").prop('value', '');
						$("#grade").prop('value', '');
						
						$("#approval").prop('disabled', true);
						$("#grade").prop('disabled', true);

						$("#ocons").prop('disabled', false);
						$("#mileage").prop('disabled', false);
						$("#country").prop('disabled', false);
					}
					else {
						$("#country").prop('value', 'ES');
						$("#grade").prop('value', '');
						$("#approval").prop('value', '');
						$("#ocons").prop('disabled', true);
						$("#mileage").prop('disabled', true);
						$("#country").prop('disabled', true);
						
						$("#grade").prop('disabled', false);
						$("#approval").prop('disabled', false);
					}
				});
			} );
		</script>
