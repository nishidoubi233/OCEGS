/**
 * AI 问诊 Pinia Store (逻辑复用自参考项目)
 * AI Consultation Pinia Store (Logic reused from reference)
 */
import { defineStore } from 'pinia'
import aiDoctorApi from '@/api/aiDoctor'

export const useConsultationStore = defineStore('consultation', {
    state: () => ({
        // 当前问诊会话
        // Current consultation session
        currentConsultation: null,
        // 对话记录
        // Message history
        messages: [],
        // 最终总结
        // Final summary
        summary: null,
        // 是否正在加载/生成中
        // Is loading/generating
        loading: false,
        // 是否正在轮询步骤中
        // Is in step polling process
        isAdvancing: false,
        // 分诊结果
        // Triage result
        triageResult: null,
        // 急救指南
        // Emergency guide
        emergencyGuide: null,
        // 错误信息
        // Error message
        error: null
    }),

    getters: {
        // 问诊是否已完成
        // Is consultation finished
        isCompleted: (state) => state.currentConsultation?.status === 'completed',
        // 当前状态
        // Current status
        status: (state) => state.currentConsultation?.status || 'idle'
    },

    actions: {
        /**
         * 发起新问诊
         * Start a new consultation
         */
        async startNewConsultation(initialProblem, patientProfileId = null) {
            this.loading = true
            this.error = null
            this.messages = []
            this.summary = null

            try {
                const res = await aiDoctorApi.startConsultation({
                    initial_problem: initialProblem,
                    patient_profile_id: patientProfileId
                })
                this.currentConsultation = res.data

                // 初始消息 (主诉)
                // Initial message
                this.messages.push({
                    id: 'initial',
                    sender_type: 'patient',
                    content: initialProblem,
                    created_at: new Date().toISOString()
                })

                return res
            } catch (err) {
                this.error = 'Failed to start consultation. Please try again.'
                throw err
            } finally {
                this.loading = false
            }
        },

        /**
         * 获取现有问诊详情
         * Load existing consultation
         */
        async loadConsultation(id) {
            this.loading = true
            try {
                const res = await aiDoctorApi.getConsultation(id)
                this.currentConsultation = res.data
                this.messages = res.data.messages || []
                this.summary = res.data.summary || null
            } catch (err) {
                this.error = 'Failed to load consultation history.'
            } finally {
                this.loading = false
            }
        },

        /**
         * 自动推进整个会诊流程直到结束 (核心编排逻辑)
         * Automatically advance full process until finished
         */
        async runConsultation(consultationId) {
            if (this.isAdvancing) return
            this.isAdvancing = true

            try {
                let finished = false
                while (!finished) {
                    const res = await aiDoctorApi.advanceStep(consultationId)
                    const result = res.data

                    if (result.status === 'completed') {
                        // 完成
                        // Finished
                        await this.loadConsultation(consultationId)
                        finished = true
                    } else if (result.status === 'success') {
                        // 医生发言了，添加到列表
                        // Doctor spoke, add to list
                        this.messages.push({
                            id: Math.random().toString(36).substr(2, 9),
                            sender_type: 'doctor',
                            doctor_name: result.doctor_name,
                            doctor_id: result.doctor_id,
                            content: result.message,
                            created_at: new Date().toISOString()
                        })
                    } else if (result.status === 'transition') {
                        // 阶段切换 (如进入投票)，添加系统消息
                        // Phase transition (e.g. voting), add system message
                        this.messages.push({
                            id: Math.random().toString(36).substr(2, 9),
                            sender_type: 'system',
                            content: result.message,
                            created_at: new Date().toISOString()
                        })
                    } else if (result.error) {
                        this.error = result.error
                        finished = true
                    }

                    // 稍微延迟一下
                    // Small delay for UI smoothness
                    await new Promise(res => setTimeout(res, 800))
                }
            } catch (err) {
                this.error = 'Error during consultation process.'
            } finally {
                this.isAdvancing = false
            }
        },

        /**
         * 进行分诊评估
         * Perform triage evaluation
         */
        async triageSymptom(initialProblem) {
            this.loading = true
            this.error = null
            this.triageResult = null
            try {
                const res = await aiDoctorApi.performTriage({ initial_problem: initialProblem })
                this.triageResult = res.data
                return res.data
            } catch (err) {
                this.error = 'Failed to perform triage. Please check your network.'
                throw err
            } finally {
                this.loading = false
            }
        },

        /**
         * 获取急救指南
         * Fetch emergency guide
         */
        async fetchEmergencyGuide(consultationId) {
            this.loading = true
            this.error = null
            try {
                const res = await aiDoctorApi.getEmergencyGuide(consultationId)
                this.emergencyGuide = res.data
                return res.data
            } catch (err) {
                this.error = 'Failed to load emergency guidance.'
                throw err
            } finally {
                this.loading = false
            }
        },

        /**
         * 发送追问消息
         * Send follow-up message
         */
        async sendFollowUp(consultationId, message) {
            this.loading = true
            this.error = null
            try {
                // Add user message immediately
                this.messages.push({
                    id: `followup-${Date.now()}`,
                    sender_type: 'patient',
                    content: message,
                    created_at: new Date().toISOString()
                })

                // Send to backend
                const res = await aiDoctorApi.sendFollowUp(consultationId, message)

                // Update consultation status
                if (this.currentConsultation) {
                    this.currentConsultation.status = 'DISCUSSING'
                }

                return res.data
            } catch (err) {
                this.error = 'Failed to send follow-up message.'
                throw err
            } finally {
                this.loading = false
            }
        }
    }
})
