<template>
  <div class="tianji-container">
    <div class="header">
      <h1>天玑推演系统</h1>
      <p class="subtitle">Oriental Philosophy Enhanced Multi-Agent Simulation</p>
    </div>

    <!-- 输入表单 -->
    <div class="input-panel">
      <div class="form-section">
        <h3>基础信息</h3>
        <div class="form-row">
          <label>问题描述</label>
          <textarea v-model="form.question" placeholder="请输入您想推演的问题..." rows="3" />
        </div>
        <div class="form-row">
          <label>领域</label>
          <select v-model="form.domain">
            <option value="strategy">战略决策</option>
            <option value="relationship">情感关系</option>
            <option value="business">商业决策</option>
            <option value="content">内容传播</option>
            <option value="personal">个人发展</option>
          </select>
        </div>
        <div class="form-row">
          <label>目标</label>
          <input v-model="form.goal" placeholder="例如：判断发布时机" />
        </div>
      </div>

      <div class="form-section">
        <h3>时间与地点（可选）</h3>
        <div class="form-row-split">
          <div>
            <label>事件时间</label>
            <input v-model="form.event_time" type="datetime-local" />
          </div>
          <div>
            <label>地点</label>
            <input v-model="form.location" placeholder="例如：Guangzhou" />
          </div>
        </div>
      </div>

      <div class="form-section">
        <h3>出生信息（可选，用于四柱分析）</h3>
        <div class="form-row-split">
          <div>
            <label>出生时间</label>
            <input v-model="form.birth_datetime" type="datetime-local" />
          </div>
          <div>
            <label>性别</label>
            <select v-model="form.gender">
              <option value="">未知</option>
              <option value="male">男</option>
              <option value="female">女</option>
            </select>
          </div>
        </div>
      </div>

      <div class="form-actions">
        <button class="btn-primary" @click="runSimulation" :disabled="loading">
          {{ loading ? '推演中...' : '开始推演' }}
        </button>
        <button class="btn-secondary" @click="clearAll">清空</button>
      </div>
    </div>

    <!-- 加载状态 -->
    <div v-if="loading" class="loading">
      <div class="spinner"></div>
      <p>天玑系统推演中，请稍候...</p>
    </div>

    <!-- 报告输出 -->
    <div v-if="report" class="report-panel">
      <div class="report-header">
        <h2>推演报告</h2>
        <span class="report-id">ID: {{ report.report_id }}</span>
      </div>

      <!-- 总断 -->
      <div class="report-section total">
        <h3>总断</h3>
        <p>{{ report.strategy.best_action }}</p>
        <div class="confidence">
          置信度：<span :class="report.confidence.level">{{ report.confidence.level }} ({{ report.confidence.value }}%)</span>
        </div>
      </div>

      <!-- 象数建模 -->
      <div class="report-section">
        <h3>象数建模</h3>
        <div class="symbolic-grid">
          <div class="symbolic-item">
            <span class="label">八卦</span>
            <span class="value">{{ report.symbolic.bagua.main }}</span>
          </div>
          <div class="symbolic-item">
            <span class="label">五行</span>
            <span class="value">{{ report.symbolic.wuxing.main }}</span>
          </div>
          <div class="symbolic-item">
            <span class="label">易经</span>
            <span class="value">{{ report.symbolic.iching.primary_hexagram.name }} → {{ report.symbolic.iching.changed_hexagram.name }}</span>
          </div>
          <div v-if="report.symbolic.bazi.status === 'ok'" class="symbolic-item">
            <span class="label">四柱</span>
            <span class="value">
              {{ report.symbolic.bazi.pillars.year }} {{ report.symbolic.bazi.pillars.month }} {{ report.symbolic.bazi.pillars.day }} {{ report.symbolic.bazi.pillars.hour }}
            </span>
          </div>
          <div v-if="report.symbolic.qimen.status === 'ok'" class="symbolic-item">
            <span class="label">奇门</span>
            <span class="value">{{ report.symbolic.qimen.bureau.label }}</span>
          </div>
        </div>
      </div>

      <!-- 四柱详情 -->
      <div v-if="report.symbolic.bazi.status === 'ok' && report.symbolic.bazi.v3_precision" class="report-section">
        <h3>四柱精密分析</h3>
        <div class="bazi-detail">
          <p><strong>日主：</strong>{{ report.symbolic.bazi.day_master.stem }}{{ report.symbolic.bazi.day_master.element }}</p>
          <p><strong>身强：</strong>{{ report.symbolic.bazi.strong_weak }}</p>
          <p><strong>用神：</strong>{{ report.symbolic.bazi.v3_precision.useful_god.stems.join('、') }}</p>
          <p><strong>忌神：</strong>{{ report.symbolic.bazi.v3_precision.forbidden_god.stems.join('、') }}</p>
          <p><strong>月令：</strong>{{ report.symbolic.bazi.v3_precision.month_correction }}</p>
        </div>
      </div>

      <!-- 奇门详情 -->
      <div v-if="report.symbolic.qimen.status === 'ok' && report.symbolic.qimen.v3_precision" class="report-section">
        <h3>奇门精密分析</h3>
        <div class="qimen-detail">
          <p><strong>值符：</strong>{{ report.symbolic.qimen.v3_precision.value_fu.palace }}</p>
          <p><strong>值使：</strong>{{ report.symbolic.qimen.v3_precision.value_shi.palace }}</p>
          <p><strong>天盘：</strong>{{ Object.entries(report.symbolic.qimen.v3_precision.heaven_plate).slice(0,4).map(e => e[0]+e[1]).join(' ') }}</p>
          <p><strong>马星：</strong>{{ report.symbolic.qimen.v3_precision.horse_star }}</p>
          <p><strong>空亡：</strong>{{ report.symbolic.qimen.v3_precision.empty_palaces.slice(0,4).join('、') }}</p>
        </div>
      </div>

      <!-- 易经详情 -->
      <div v-if="report.symbolic.iching.v3_precision" class="report-section">
        <h3>易经精密分析</h3>
        <div class="iching-detail">
          <p><strong>错卦：</strong>{{ report.symbolic.iching.v3_precision.错卦_cuo.name }}</p>
          <p><strong>互卦：</strong>{{ report.symbolic.iching.v3_precision.互卦_nuclear.name }}</p>
          <p><strong>六亲：</strong>{{ report.symbolic.iching.v3_precision.liu_qin.map(l => l.position+l.relation).join(' ') }}</p>
        </div>
      </div>

      <!-- 未来路径 -->
      <div class="report-section">
        <h3>未来分支路径</h3>
        <div class="branch-list">
          <div v-for="(branch, idx) in report.future.branches" :key="idx" class="branch-item">
            <div class="branch-header">
              <span class="branch-name">{{ branch.name }}</span>
              <span class="branch-prob">{{ (branch.probability * 100).toFixed(0) }}%</span>
            </div>
            <p class="branch-outcome">{{ branch.outcome }}</p>
            <p class="branch-trigger"><strong>触发：</strong>{{ branch.trigger_conditions.join('；') }}</p>
          </div>
        </div>
      </div>

      <!-- 禁忌 -->
      <div v-if="report.strategy.forbidden_actions.length" class="report-section forbidden">
        <h3>禁忌动作</h3>
        <ul>
          <li v-for="(action, idx) in report.strategy.forbidden_actions" :key="idx">{{ action }}</li>
        </ul>
      </div>

      <!-- 观察信号 -->
      <div v-if="report.strategy.watch_signals.length" class="report-section">
        <h3>观察信号</h3>
        <ul>
          <li v-for="(signal, idx) in report.strategy.watch_signals" :key="idx">{{ signal }}</li>
        </ul>
      </div>

      <!-- 置信度 -->
      <div class="report-section">
        <h3>置信度与盲区</h3>
        <div class="confidence-detail">
          <p><strong>置信度：</strong>{{ report.confidence.value }}% ({{ report.confidence.level }})</p>
          <p><strong>盲区：</strong>{{ report.confidence.blindspots.join('；') }}</p>
        </div>
      </div>

      <!-- 回填反馈 -->
      <div class="report-section review">
        <h3>推演反馈回填</h3>
        <div class="review-form">
          <div class="form-row">
            <label>实际发生了什么？</label>
            <textarea v-model="review.actual_outcome" placeholder="请描述实际发生的结果..." rows="2" />
          </div>
          <div class="form-row">
            <label>预测准确度</label>
            <select v-model="review.accuracy">
              <option value="">请选择</option>
              <option value="accurate">完全准确</option>
              <option value="mostly_accurate">大部分准确</option>
              <option value="partially_accurate">部分准确</option>
              <option value="wrong">不准确</option>
            </select>
          </div>
          <div class="form-row">
            <label>偏差分析（可选）</label>
            <textarea v-model="review.deviation_analysis" placeholder="哪些预测有偏差？" rows="2" />
          </div>
          <button class="btn-primary" @click="submitReview" :disabled="reviewLoading">
            {{ reviewLoading ? '提交中...' : '提交反馈' }}
          </button>
          <p v-if="reviewSuccess" class="success-msg">反馈已保存！</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'TianJiView',
  data() {
    return {
      form: {
        question: '',
        domain: 'strategy',
        goal: '',
        event_time: '',
        location: '',
        birth_datetime: '',
        gender: ''
      },
      loading: false,
      report: null,
      review: {
        actual_outcome: '',
        accuracy: '',
        deviation_analysis: ''
      },
      reviewLoading: false,
      reviewSuccess: false
    }
  },
  methods: {
    async runSimulation() {
      if (!this.form.question.trim()) {
        alert('请输入问题描述')
        return
      }
      this.loading = true
      this.report = null
      this.reviewSuccess = false
      try {
        const payload = {
          question: this.form.question,
          domain: this.form.domain,
          goal: this.form.goal || undefined,
          event_time: this.form.event_time ? this.form.event_time.replace('T', ' ') : undefined,
          location: this.form.location || undefined,
          birth_datetime: this.form.birth_datetime ? this.form.birth_datetime.replace('T', ' ') : undefined,
          gender: this.form.gender || undefined,
          rounds: 3,
          save_report: true
        }
        const resp = await axios.post('/api/tianji/run', payload)
        this.report = resp.data.data || resp.data
      } catch (err) {
        alert('推演失败：' + (err.response?.data?.message || err.message))
      } finally {
        this.loading = false
      }
    },
    async submitReview() {
      if (!this.review.actual_outcome.trim() || !this.review.accuracy) {
        alert('请填写实际结果和准确度')
        return
      }
      this.reviewLoading = true
      try {
        await axios.post('/api/tianji-review/submit', {
          report_id: this.report.report_id,
          actual_outcome: this.review.actual_outcome,
          accuracy: this.review.accuracy,
          deviation_analysis: this.review.deviation_analysis
        })
        this.reviewSuccess = true
        setTimeout(() => { this.reviewSuccess = false }, 3000)
      } catch (err) {
        alert('提交失败：' + (err.response?.data?.message || err.message))
      } finally {
        this.reviewLoading = false
      }
    },
    clearAll() {
      this.form = { question: '', domain: 'strategy', goal: '', event_time: '', location: '', birth_datetime: '', gender: '' }
      this.report = null
      this.review = { actual_outcome: '', accuracy: '', deviation_analysis: '' }
      this.reviewSuccess = false
    }
  }
}
</script>

<style scoped>
.tianji-container { max-width: 900px; margin: 0 auto; padding: 24px; font-family: 'PingFang SC', 'Microsoft YaHei', sans-serif; }
.header { text-align: center; margin-bottom: 32px; border-bottom: 2px solid #1a1a2e; padding-bottom: 16px; }
.header h1 { font-size: 28px; color: #1a1a2e; margin: 0 0 8px; }
.subtitle { color: #666; font-size: 14px; margin: 0; }
.input-panel { background: #f8f9fa; border-radius: 12px; padding: 24px; margin-bottom: 24px; }
.form-section { margin-bottom: 20px; }
.form-section h3 { font-size: 16px; color: #1a1a2e; margin: 0 0 12px; border-left: 3px solid #16213e; padding-left: 8px; }
.form-row { margin-bottom: 12px; }
.form-row label { display: block; font-size: 13px; color: #555; margin-bottom: 4px; font-weight: 500; }
.form-row textarea, .form-row input, .form-row select { width: 100%; padding: 8px 12px; border: 1px solid #ddd; border-radius: 6px; font-size: 14px; box-sizing: border-box; font-family: inherit; }
.form-row textarea:focus, .form-row input:focus, .form-row select:focus { outline: none; border-color: #16213e; }
.form-row-split { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }
.form-row-split > div label { display: block; font-size: 13px; color: #555; margin-bottom: 4px; font-weight: 500; }
.form-row-split > div input, .form-row-split > div select { width: 100%; padding: 8px 12px; border: 1px solid #ddd; border-radius: 6px; font-size: 14px; box-sizing: border-box; }
.form-actions { display: flex; gap: 12px; }
.btn-primary { background: #16213e; color: #fff; border: none; padding: 10px 24px; border-radius: 6px; font-size: 15px; cursor: pointer; font-weight: 500; }
.btn-primary:disabled { background: #999; cursor: not-allowed; }
.btn-secondary { background: #fff; color: #16213e; border: 1px solid #16213e; padding: 10px 24px; border-radius: 6px; font-size: 15px; cursor: pointer; }
.loading { text-align: center; padding: 48px; color: #666; }
.spinner { width: 40px; height: 40px; border: 3px solid #e0e0e0; border-top-color: #16213e; border-radius: 50%; animation: spin 0.8s linear infinite; margin: 0 auto 16px; }
@keyframes spin { to { transform: rotate(360deg); } }
.report-panel { background: #fff; border-radius: 12px; padding: 24px; border: 1px solid #e0e0e0; }
.report-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; padding-bottom: 12px; border-bottom: 1px solid #eee; }
.report-header h2 { font-size: 20px; color: #1a1a2e; margin: 0; }
.report-id { font-size: 12px; color: #999; font-family: monospace; }
.report-section { margin-bottom: 20px; padding: 16px; background: #f8f9fa; border-radius: 8px; }
.report-section h3 { font-size: 15px; color: #16213e; margin: 0 0 12px; font-weight: 600; }
.total { background: linear-gradient(135deg, #16213e 0%, #0f3460 100%); color: #fff; }
.total h3 { color: #e8d5b7; }
.total p { font-size: 16px; line-height: 1.6; margin: 0 0 8px; }
.confidence { font-size: 13px; color: rgba(255,255,255,0.8); }
.symbolic-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(180px, 1fr)); gap: 8px; }
.symbolic-item { background: #fff; padding: 8px 12px; border-radius: 6px; display: flex; flex-direction: column; gap: 2px; }
.symbolic-item .label { font-size: 12px; color: #999; }
.symbolic-item .value { font-size: 14px; color: #1a1a2e; font-weight: 500; }
.bazi-detail p, .qimen-detail p, .iching-detail p, .confidence-detail p { margin: 4px 0; font-size: 14px; color: #444; }
.branch-list { display: flex; flex-direction: column; gap: 12px; }
.branch-item { background: #fff; padding: 12px 16px; border-radius: 8px; border-left: 3px solid #16213e; }
.branch-header { display: flex; justify-content: space-between; margin-bottom: 6px; }
.branch-name { font-weight: 600; color: #1a1a2e; font-size: 14px; }
.branch-prob { background: #16213e; color: #fff; padding: 2px 8px; border-radius: 12px; font-size: 12px; }
.branch-outcome { margin: 4px 0; font-size: 14px; color: #444; }
.branch-trigger { margin: 4px 0; font-size: 13px; color: #888; }
.forbidden { border-left: 3px solid #c0392b; }
.forbidden ul { margin: 0; padding-left: 20px; color: #c0392b; font-size: 14px; }
.forbidden li { margin: 4px 0; }
.report-section ul { margin: 0; padding-left: 20px; font-size: 14px; color: #555; }
.report-section li { margin: 4px 0; }
.review { border: 2px dashed #16213e; background: #fff; }
.review h3 { color: #16213e; }
.success-msg { color: #27ae60; font-size: 14px; margin: 8px 0 0; }
.high { color: #27ae60; }
.medium { color: #f39c12; }
.low { color: #e74c3c; }
</style>
