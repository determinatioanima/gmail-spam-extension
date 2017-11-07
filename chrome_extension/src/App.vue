<template>
<div>
	<div class="ui first couple modal">
	    <div class="ui dividing header">
	        Report the E-mail.
	    </div>
	    <div class="content">
		    <div class="actions">
		        <div class="ui form">
					<!-- Q1 -->
					<div class="inline fields">
						<label>The level of the hazard.</label>
						<div class="field">
							<div class="ui radio checkbox">
								<input type="radio" name="f_1" checked="checked">
								<label>High</label>
							</div>
						</div>
						<div class="field">
							<div class="ui radio checkbox">
								<input type="radio" name="f_1">
								<label>Medium</label>
							</div>
						</div>
						<div class="field">
							<div class="ui radio checkbox">
								<input type="radio" name="f_1">
								<label>Low</label>
							</div>
						</div>
					</div>
					<!-- Q2 -->
					<div class="inline fields">
						<label>How often do you use email?</label>
						<div class="field">
							<div class="ui radio checkbox">
								<input type="radio" name="f_2" checked="checked">
								<label>Once a week</label>
							</div>
						</div>
						<div class="field">
							<div class="ui radio checkbox">
								<input type="radio" name="f_2">
								<label>2-3 times a week</label>
							</div>
						</div>
						<div class="field">
							<div class="ui radio checkbox">
								<input type="radio" name="f_2">
								<label>Once a day</label>
							</div>
						</div>
						<div class="field">
							<div class="ui radio checkbox">
								<input type="radio" name="f_2">
								<label>Twice a day</label>
							</div>
						</div>
					</div>
					<!-- Q3 -->
					<div class="inline fields">
						<label>Please select one category.</label>
						<div class="field">
							<div class="ui radio checkbox">
								<input type="radio" name="f_3" checked="checked">
								<label>Normal</label>
							</div>
						</div>
						<div class="field">
							<div class="ui radio checkbox">
								<input type="radio" name="f_3">
								<label>Fraud</label>
							</div>
						</div>
						<div class="field">
							<div class="ui radio checkbox">
								<input type="radio" name="f_3">
								<label>Trash</label>
							</div>
						</div>
						<div class="field">
							<div class="ui radio checkbox">
								<input type="radio" name="f_3">
								<label>Malicious</label>
							</div>
						</div>
					</div>

					<div class="ui form">
						<div class="field">
							<label>Details</label>
							<textarea rows="2"></textarea>
						</div>

						<div class="ui buttons">
							<button class="ui positive button SEND">Send</button>
							<div class="or"></div>
							<button class="ui button CANCEL">Cancel</button>
						</div>
					</div>
		        </div>
			</div>
	    </div>
	</div>

	<div class="ui mini second couple modal">
		<div class="ui content">
	        <div class="ui form">
				<div class="field">
					<label>Thanks for reporting.</label>
					<button class="positive ui button OK">OK</button>
				</div>
			</div>
		</div>
	</div>

	<div id="INFO" class="ui small modal">
			<div class="ui three column divided center aligned grid">
				<div class="column">
					<h4 class="ui header">分數</h4>
					<p id="PSCORE"></p>
				</div>
				<div class="column">
					<h4 class="ui header">來源可靠</h4>
					<p id="PSPF"></p>
				</div>
				<div class="column">
					<h4 class="ui header">確定未遭串改</h4>
					<p id="PDKIM"></p>
				</div>
				<div class="column">
					<h4 class="ui header">有回報機制</h4>
					<p id="PDMARC"></p>
				</div>
				<div class="column">
					<h4 class="ui header">附加檔案</h4>
					<p id="PATTACHED"></p>
				</div>
				<div class="column">
					<h4 class="ui header">內容</h4>
					<p id="PCONTENT"></p>
				</div>
		</div>
	</div>

</div>
</template>

<script>
export default {
  name: 'contentUI',
  data () {
    return {
      toggle: 'false'
    }
  },
  watch: {

  },
  methods: {

  },
  mounted: function(){

  }
}
</script>

<style scoped>

</style>
